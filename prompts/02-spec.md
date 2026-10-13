# Phase 2 · Spec

**Model:** Opus 5.5 — at effort `xhigh` (`claude --model claude-opus-5-5 --effort xhigh`); the highest reasoning demand, little output.
**Result:** `plans/changes/<name>/spec.md`
**Gate:** the interview check green for this change — `python3
scripts/check_interview_minimums.py --change <name>`; phase 1a has met its
minimum or holds its skip record — plus `python3
scripts/validate_change_artefacts.py --check` green, and no open
`[DECISION]`.

You describe **what** shall hold — not how it is built.

Write `spec.md` in the form of `templates/spec.md`: copy it into the change folder and fill it in.

**You do not interview here.** Phase 1a did that, and its answers are in
`decisions.md`. This phase synthesises what `research.md` and `decisions.md`
already say. If you find yourself needing an answer that is in neither, that is
a `[DECISION]` — see below — not a question to slip into the prose.

Required sections:

- **Problem.** What does not work today, with evidence from `research.md`.
- **Acceptance criteria.** Checkable sentences, one condition each; where a
  trigger, a state or a failure applies, the sentence begins with When, While or
  If. Each one comes with what would *refute* it. A criterion that cannot go red
  is not one.
- **Non-goals.** What explicitly does not belong. Without this section the scope
  grows during implementation and nobody can say from when.
- **Open decisions.** Classify first, then ask.

## Classify before you ask

```
[DECISION] → human   irreversible · external contract · risk · or two plausible
                     readings of what was asked for
[GAP]      → explore answerable from the repository → extend research.md,
                     do not ask
[DETAIL]   → agent   freely revisable → decide it, record the reason
```

What is reversible and binds nothing beyond this change — wording, demonstration
values, test seeds, ordering, numbering proposals — **you decide yourself**: the
decision and its reason go in this section, and you say so in one sentence. A
default chosen *silently* is the decision that should have stayed visible; a
written one is visible.

## The form of a `[DECISION]`

It is answerable by someone who has not read the code. Never a mechanism
question — those are `[DETAIL]` or `[GAP]`, and asking one of an intent owner is
a protocol violation, not thoroughness.

```
Goal in one sentence:  <what this is about, in plain words>
Options:               each named after what it does, with its consequence
                       for users, operations or risk — not its mechanism
Recommendation:        <one option> — because <one sentence>
If you say "ok":       <exactly what will then be built>
What is lost:          <what the other option would have given>
```

Answers are: **ok** · **option N** · **change criterion N to "…"** · **no,
because …**. That is the decision record (MADR) in question form. Shorthand
(work item, A-/G-point, invariant) only as a trailing note, never carrying the
sentence. You ask only once all of the above stands.

Frontmatter per `plans/_README.md`: `status`, `implementation_status`, `date`,
`last_reviewed`, `bead`. Also `class:` — one of `spike`, `bounded`, `feature`,
`architectural` (`docs/WORKFLOW.md`, "Change classes, the ADR question and
decision pull requests"). For a `feature`, also `change: <folder name>` and
`adr_question: {proposed: "yes"|"no", reason: "<one sentence>"}` — quote
`"yes"` and `"no"`: bare, YAML reads them as booleans, and the gate
`adr-answers` refuses the header. The proposal only proposes; the maintainer
answers, with `python3 scripts/harness.py decide adr`.

Every class lists under `adr_files: [docs/adr/<file>, …]` each file under
`docs/adr/` the change creates, changes or removes — `[]` or no line when it
touches none. The header lists every ADR file the change touches: the gate
`interview-minimums` attributes an ADR edit to that claim alone and holds a
feature's answer to it, "yes" with at least one claimed file and "no" with none
(ADR 0014, `docs/WORKFLOW.md`).

## After the spec review

Phase 2a returns its rows in `findings.md`. Before phase 3 starts, you work
each of them into `spec.md` itself: a hole is closed, a criterion that cannot
go red gets its refuting case. A row you do not take over gets its reason in
`findings.md`. An `[AMBIGUITY]` goes to the person, and their answer goes into
the spec. Each 2a row then says `in spec` or `rejected — <reason>`; none stays
open. The revised `spec.md` is the one yardstick from here on: plan, code and
the phase 6 review measure against it, not against the 2a rows.
