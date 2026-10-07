# Phase 2a · Spec review

**Model:** Opus 5.5 — for a spike, in a fresh context that never saw the
author's reasoning; for a bounded, feature or architectural change gpt-6.1-sol
at effort `max`, started by `python3 scripts/stage2.py spec-review <change>`.
**Input:** `spec.md`, `research.md`, `decisions.md`. **Not** the author's reasoning.
**Result:** rows for `plans/changes/<name>/findings.md`, dimension `SPEC`.
**Gate:** no open `[AMBIGUITY]`.
**Session:** the same reviewer later runs phase 6. On the Claude path (Opus 5.5),
start it with a fixed id, `claude --model claude-opus-5-5 --session-id <uuid>
-n review-<name>`, and write the id under the table in `findings.md`
(`Reviewer session: <uuid>`). On the Codex path the runner starts the session
and writes `Reviewer session: codex <thread id>` itself.

Through the runner you answer in table rows of six cells — `| ID | Severity |
Dimension | Origin | Where | Finding |` — and the runner adds the reviewer, the
status and the session line (`docs/WORKFLOW.md` §4). Write a `|` inside a cell
as `\|`.

A validator checks that the sections are there. It cannot check that they say
the right thing. A clean, complete spec describing the wrong thing passes every
mechanical gate there is — and the cost of that shows up in phase 4, where it is
twenty times more expensive.

So you read the spec before anything is built, and you answer **three questions
and nothing else**:

1. **Where does this admit two plausible readings?**
   Not "this is unclear" — name both readings and say what each would produce.
   Every one of these is `[AMBIGUITY]`, and the human settles it, never you.

2. **What is missing that would have to be decided while building?**
   The test: could someone implement this without inventing something the spec
   is silent about? Where they could not, the spec has a hole, and it will be
   filled silently unless you name it now.

3. **Which acceptance criterion cannot go red?**
   For each one, state the input and the state that would refute it. Where you
   cannot construct that case, the criterion is a statement of intent, not a
   criterion.

## What you do not do

You do not rewrite the spec. You do not propose wording. You do not judge
whether the goal is worth pursuing — that was settled in phase 1a and belongs to
a human. You do not report style.

You were not there when the spec was written, and you do not get to see how it
was reasoned. That is the point: a model rates its own derivation too kindly,
and a different model reading in a fresh context does not know by
construction that it is checking itself.

## If you find nothing

Say so, in one sentence, and name what you checked. A reviewer who always finds
something is not a stricter reviewer; it is a signal nobody can read.
