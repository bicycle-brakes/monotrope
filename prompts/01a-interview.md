# Phase 1a · Interview

**Model:** Opus 5.5 — the questions are the work, and there are few of them.
**Result:** `plans/changes/<name>/decisions.md`
**Gate:** the `interview-minimums` check green — the minimums below met, every
`[DECISION]` answered, or the phase a skip record with a reason.

Owed where a minimum stands — no longer optional. A `feature` owes at least
**three distinct, substantive** questions the maintainer answered. Creating or
changing an ADR owes **five**, whatever the class — and a feature that also
carries an ADR owes **five in total**, never the sum. A `spike` owes the three
topics — learning goal, time budget, expected outcome — or a skip with its
reason. A `bounded` change owes at least one answered question or a reasoned
skip. Where no duty stands, the skip is still written: one skip record in
`decisions.md` with its reason, never silence. What is settled stays settled —
a decision already made is not asked again, and a repeated confirmation
fulfils no minimum.

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

**Every question brings its context, written for a reader with ADHD**
(maintainer, 2026-10-14). Before the options, two to four short sentences say
what the question is about, why it comes up now and what happens today — in
plain words, without assuming the reader knows the code, the finding or an
earlier conversation. Every id or technical term is explained where it first
appears. The question itself comes last and stands on its own line.

**Stop when the design tree has no unresolved branch left.** Not when you run
out of ideas for questions. If two answers would lead to the same build, the
question was a `[DETAIL]`.

## What you write

`decisions.md`, one entry per decision. Every question the maintainer answers
becomes one **interview record** in the form the `interview-minimums` gate
counts (`scripts/check_interview_minimums.py`):

```markdown
## Q-1 · <short title>

asked: 2026-10-09
answer: <the answer, as stated>
answered_by: maintainer
status: answered

In the context of <situation>, facing <constraint>, we decided <option>,
to achieve <goal>, accepting <consequence>. — 2026-10-09
```

`status` is `answered` or `open`. Only records with `status: answered` and
`answered_by: maintainer` count toward a minimum, distinct ids, first
occurrence wins — an agent's answer, an open question and a repeated
confirmation count for nothing. When no question is owed, one **skip record**
ends the phase:

```markdown
## SKIP · interview

status: skipped
reason: <one sentence — a skip without its reason is not a skip>
```

That is the durable record. What holds beyond this change later moves unchanged
into an ADR under `docs/adr/` — which is why the form is the ADR's own.

Decisions you took yourself (`[DETAIL]`) belong here too, marked as such — as
prose paragraphs, never as Q-records. A default chosen silently is the decision
that should have stayed visible.

**Terms count.** Where the interview settles what a word means in this
repository, that belongs in `docs/glossar/` — one note per term — not in a new
file of its own. See `docs/governance/begriffs-disziplin.md`.
