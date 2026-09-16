# Phase 1a · Interview

**Model:** Fable 5.1 — the questions are the work, and there are few of them.
**Result:** `plans/changes/<name>/decisions.md`
**Gate:** every `[DECISION]` answered, or the phase recorded as skipped with a
reason.

Optional, and called by a human. Where the change fits in one sentence, skip it
— the phase overhead would eat the benefit (`docs/WORKFLOW.md`, rule 2). Skipped
is recorded in `decisions.md` as one line with the reason, not left silent.

## What this phase is

Phase 1 collected facts. Phase 2 will write the spec. Between them sits the
place where a model otherwise **guesses what was meant** — and a clean, complete
spec that describes the wrong thing passes every check there is.

So: you interview. You do not write a spec here.

The pattern is taken from [`mattpocock/skills`](https://github.com/mattpocock/skills)
(`/grill-me` → `/to-spec`): first the interview until alignment holds, then a
synthesis that does not interview again.

## How you ask

**One question at a time.** A list of twelve gets one answer for the first and
silence for the rest.

**Only questions a person can answer without reading the code.** Before asking,
classify:

```
[DECISION] → ask     irreversible · external contract · risk · or two plausible
                     readings of what was asked for
[GAP]      → read    answerable from the repository → go and read it, extend
                     research.md, do not ask
[DETAIL]   → decide  freely revisable → decide it, record the reason
```

If you cannot state a recommendation, you have a `[GAP]`, not a `[DECISION]` —
go and read first.

**Every question carries its consequence.** Not "shall we use X or Y" but "if
this happens, should the system do A or B — A means …, B means …". Options are
named after what they do to users, operations or risk, never after their
mechanism.

**Stop when the design tree has no unresolved branch left.** Not when you run
out of ideas for questions. If two answers would lead to the same build, the
question was a `[DETAIL]`.

## What you write

`decisions.md`, one entry per decision, each a Y-statement with its date:

```markdown
## D-1 · <short title>

In the context of <situation>, facing <constraint>, we decided <option>,
to achieve <goal>, accepting <consequence>. — 2026-01-01
```

That is the durable record. What holds beyond this change later moves unchanged
into an ADR under `docs/adr/` — which is why the form is the ADR's own.

Decisions you took yourself (`[DETAIL]`) belong here too, marked as such. A
default chosen silently is the decision that should have stayed visible.

**Terms count.** Where the interview settles what a word means in this
repository, that belongs in `docs/glossar/` — one note per term — not in a new
file of its own. See `docs/governance/begriffs-disziplin.md`.
