<!--
Template for a change's findings file. Copy it to
`plans/changes/<change>/findings.md` and fill it in. Everything from the line
`---` near the end down is reference and is not copied. This comment is not
copied either.

1. The yaml block below is the header of the copy: put its lines between two
   `---` lines at the top and replace every `<...>`. It carries no header of
   its own here (`provenance.yaml`, prefix `templates/`). In the body a
   placeholder stands in backticks, so that GitHub shows it: replace it,
   backticks included.
2. One row per finding. The table is the answer of a review: its columns stand
   exactly as shown (`prompts/06-review.md`, `prompts/02a-spec-review.md`).
   Rows of the spec review (phase 2a) and of the review (phase 6) go into the
   same table; a row is not deleted, its Status moves.
-->

```yaml
title: "Findings — <change>"
category: findings
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
status: draft
implementation_status: none
date: <YYYY-MM-DD>
last_reviewed: <YYYY-MM-DD>
supersedes: null
superseded_by: null
bead: <bead id>
owner: <role>
provenance: ai-drafted-reviewed
produced_by: {kind: llm-session, name: <agent>, version: "<YYYY-MM-DD>"}
review: {status: pending, approved_by: null, approved_at: null}
tags: [findings, <topic>]
```

# Findings — `<change>`

Phase `<phase>`, on commit `<commit>`, `<YYYY-MM-DD>`, read by `<who read it and
in what context>`. One sentence on what the rows were measured against, and the
verdict: how many rows of which severity, and whether any `[AMBIGUITY]` or
`[DIVERGENT]` stands.

| ID | Severity | Dimension | Origin | Where | Finding | Status |
|---|---|---|---|---|---|---|
| F-1 | MINOR | SPEC | base | `spec.md`, criterion 3 | What is wrong, and the case that shows it. | open |

Reviewer session: `<id>`

## Checked without a finding

What was read and held, each with where — so that "no finding" is a statement
and not a silence.

## Not checked

What was not read or not run, each with why. "Not checked" is not "no finding".

---

Reference — what the columns and markers mean. Not copied.

**Severity**

- `BLOCKER` — the change violates the spec, or a defect is demonstrated. Open,
  it stops the change at phase 6.
- `MAJOR` — substantial, but not a violation of the spec. A person decides per
  row.
- `MINOR` — cosmetics, a suspicion, an improvement. Never blocks.

**Dimension**

- `SPEC` — measured against `spec.md`: what was promised and not built.
- `MAINT` — the eye of a maintainer who was not there: error handling, edge
  cases, contracts facing outward, security. What the spec is silent about.

**Origin**

- `base` — the finding existed before the last repair.
- `fix-r<N>` — repair round N produced it. Two consecutive rounds of `fix-r`
  origin are an escalation, not a third round.

**Markers that override everything**

- `[AMBIGUITY]` — the spec or plan admits two plausible readings. It is never
  decided locally: a person sets the reading.
- `[DIVERGENT]` — two places answer the same question in opposite ways. A
  `[DIVERGENT]` counts as a `BLOCKER`, however harmless each line looks alone.

**A finding rejected before** returns only with new evidence attached.
Repetition without new evidence is not a finding.

**Status** — the values in use, not a closed set. Each may be followed by a
dash and a note:

- `open` — found, nothing done.
- `fixed in <commit>` — repaired, with the commit.
- `resolved <date> by <source>` — settled by a decision, with its source.
- `answered` — a question of the spec review, answered in phase 6.
- `in spec` — a spec-review row that arrived in `spec.md`.
- `rejected — <reason>` — not taken over, with the reason.

**Stage 2** (dated 2026-09-30). Once pull request #60 is merged,
`docs/WORKFLOW.md` §4 defines what follows, and a change that runs stage 2
adds it. Until then no change carries any of it, and the columns above are the
only ones. The forms, as that pull request's runner `scripts/stage2.py` writes
them:

```text
| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test |
| ID | Severity | Dimension | Origin | Where | Finding | Reviewer | Status | Broke a test | Phase 6 |
```

The second header is for released rows. The Status of a loop row is
`taken — <test or criterion>` or `rejected — <reason>`. Lines:

```text
Reviewer session: codex <id>
Phase 6 verdict: <reviewer> <session>, <date>
Stage-2 call, <date>: <verb> · endpoint <endpoint> · model <model> · leak check clean over <n> files, <n> commits, <n> rules.
```

The released loop rows stand in a section of their own, and the section holds
the line `Rounds run: <n>`:

```text
## Phase 4b — loop rows, released <date>
Rounds run: <n>
```

When the loop did not run there is no section and no heading. The runner puts
one line in its place, at the end of the file:

```text
Loop rows: none — the loop did not run for this change.
```
