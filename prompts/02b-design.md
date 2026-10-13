# Phase 2b · Design

**Model:** gpt-6.1-sol — Codex (`gpt-6.1-sol`) at effort `max`, started by
`python3 scripts/stage2.py draft <change>`: one call writes spec, design and
plan (phases 2, 2b and 3), and GLM 5.3 after two failed attempts; the same
demand as spec and plan. Where Stage 2 is off, Opus 5.5 at effort `xhigh`
(`claude --model claude-opus-5-5 --effort xhigh`) writes it.
**Input:** `spec.md` as revised after phase 2a, `research.md`, `decisions.md`.
**Result:** `plans/changes/<name>/design.md`
**Gate:** `python3 scripts/plans_registry.py --check` green, and for an
`architectural` change an ADR draft in `design.md`.

You decide **how the system is shaped** — between what the spec says shall hold
and how the plan builds it. Which alternatives were weighed, what crosses a
boundary, what is stored, and what the architecture looks like after the change.

## When this phase runs

Decision D-14 sets it by the change's class (`class:` in the spec header):

- `architectural` — always.
- `feature` — either the phase, or one sentence in `spec.md` saying why not.
- `bounded` — never.
- `spike` — never.

Nothing checks this rule until the change-artefact validator lands (bead
coding-harness-jc3); the review before the merge holds it.

## What `design.md` holds

Write `design.md` in the form of `templates/design.md`: copy it into the change
folder and fill it in. The template carries the five parts and says what each
asks for; this prompt does not repeat it. A part with nothing to say says why in
one sentence.

## The ADR draft

For an `architectural` change, and for a `feature` whose spec proposes "yes" to
the ADR question or whose answer is "yes" (the answer often comes only at the
merge, so the proposal is what this phase can know), the draft takes the form of
`templates/adr.md`. It becomes `docs/adr/<NNNN>-<slug>.md` in the change's own
pull request, which makes that pull request a decision pull request
(`docs/WORKFLOW.md`, "Change classes, the ADR question and decision pull
requests"). The chosen alternative is a proposal: the merge decides it (ADR
0008).

## From design to plan

Phase 3 plans from `spec.md` and `design.md` and writes into `plan.md` what
phase 4 needs from the design: phase 4 still reads `plan.md` and `spec.md` and
nothing else.

## Questions

Classify before you ask (`docs/WORKFLOW.md`):

```
[DECISION] → human   irreversible · external contract · risk · or the spec
                     admits two plausible readings
[GAP]      → explore answerable from the repository → extend research.md
[DETAIL]   → agent   freely revisable → decide it, record the reason
```

A `[DECISION]` at this stage means the spec did not settle something the design
cannot avoid. It goes back to `decisions.md`, not into the design as an aside.
