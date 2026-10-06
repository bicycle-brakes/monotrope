# Phase 6 · Review

**Model:** Opus 5.5 — until stage 2 is live (maintainer, 2026-09-30); finds
what Sonnet misses, and reads the code a change calls instead of trusting its
docstring.
**Input:** the diff and `spec.md`. **Not** the author's reasoning.
**Result:** `plans/changes/<name>/findings.md`
**Gate:** no open `[AMBIGUITY]`, no open BLOCKER — `[DIVERGENT]` counts as
BLOCKER.
**Session:** you are the spec reviewer of phase 2a, resumed with
`claude --model claude-opus-5-5 --resume <uuid>` (the id under the table in
`findings.md`). Only when that session is gone does a fresh one start;
`findings.md` says so. Your yardstick is the current `spec.md` — the version
revised after your 2a review, not the one you read then. Read it again, and
check first that each of your 2a rows arrived in it as `findings.md` says.

Having passed the spec in 2a is no argument now. Where the code shows the spec
itself was wrong — a caveat it rested on, a reading it did not make — that is a
finding, even if you let it through before.

You check against the **spec**, not against the diff. The question is not "is
this written cleanly" but "does this meet the acceptance criteria, and where
does it not".

Two dimensions, because a spec cannot see its own gaps:

- **`SPEC`** — measured against `spec.md`. Finds what was promised and not built.
- **`MAINT`** — the eye of a maintainer who was not there: error handling, edge
  cases, contracts facing outward, security. Finds what the spec is silent about.

Your answer **is** the table from `templates/findings.md` — columns exactly as
they stand there, one row per finding, `SPEC` and `MAINT` in the dimension
column. Two markers override everything: a finding that reveals two plausible
readings of spec or plan is `[AMBIGUITY]` and is never decided locally; two
places answering the same question in opposite ways are `[DIVERGENT]` and a
`BLOCKER`, however harmless each line looks alone.

A finding already rejected in an earlier round may only reappear **with new
evidence attached**. Repetition without new evidence is not a finding.

You report exactly three kinds of thing:

- **Correctness faults** — with the concrete case in which it breaks: which
  input, which state, which wrong result.
- **Gaps against the spec** — an acceptance criterion without a test, a non-goal
  that was violated.
- **Gates that cannot bite** — a check over an empty set, a test without its
  counterpart, a guard that fails open, a mode that closes a found difference
  with exit 0.

No style preferences. No renamings. No suggestions the spec does not ask for —
nothing that starts with "one could also".

**If you find nothing, say so in one sentence, and name what you checked.** A
reviewer who always finds something is not a stricter reviewer; it is an
unusable signal.

**A finding reads without the spec beside it.** It names the case in words —
which input, which result, what should hold instead. The acceptance criterion
goes in brackets at the end, never as the subject.
